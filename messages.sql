-- selects all handles w/ their corresponding info about the contact they represent
SELECT
    ROWID AS handle_id,
    id AS full_number,
    country,
    service,
    person_centric_id AS person_id
FROM handle;


-- selects all chats w/ their corresponding info
SELECT
    ROWID AS chat_id,
    account_id,
    service_name AS service
    style,
    group_id
FROM chat;


-- selects all messages & formats their date
SELECT
    ROWID AS id,
    text,
    is_from_me,
    datetime((date/1000000000) + strftime('%s', '2001-01-01 00:00:00'), 'unixepoch', 'localtime') AS date
FROM message
ORDER BY date DESC;


-- combined query
-- accounts for empty texts (likely attachments)
-- dedupes texts sent as iMessage & SMS (presumably, due to lack of service)
SELECT
    m.ROWID AS message_id, cmj.chat_id AS chat_id, m.handle_id AS handle_id,
    h.id AS phone_number, text, is_from_me,
    style AS chat_style, m.service AS service, group_id, person_centric_id AS persion_id,
    datetime((date/1000000000) + strftime('%s', '2001-01-01 00:00:00'), 'unixepoch', 'localtime') AS date
FROM message AS m
INNER JOIN chat_message_join AS cmj
    ON cmj.message_id = m.ROWID
INNER JOIN chat AS c
    ON cmj.chat_id = c.ROWID
LEFT JOIN handle AS h
ON m.handle_id = h.ROWID
WHERE text IS NOT NULL
GROUP BY message_id;


-- selects imessage/sms duplicates in chat_message_join
SELECT chat_id, message_id, COUNT(*)
FROM chat_message_join
GROUP BY message_id
HAVING COUNT(*) > 1;
