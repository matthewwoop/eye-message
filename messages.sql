-- selects all messages w/ their corresponding chat id
SELECT cmj.message_id AS message_id, cmj.chat_id AS chat_id, text, is_from_me, datetime((date/1000000000) + strftime('%s', '2001-01-01 00:00:00'), 'unixepoch', 'localtime') AS date
FROM chat_message_join AS cmj
INNER JOIN message AS m
ON cmj.message_id = m.ROWID
ORDER BY date;


-- selects all handles w/ their corresponding chats
SELECT chj.handle_id AS handle_id, chj.chat_id AS chat_id,
id AS full_number, country, service, uncanonicalized_id AS local_number, person_centric_id AS person_id
FROM chat_handle_join AS chj
INNER JOIN handle AS h
ON chj.handle_id = h.ROWID
ORDER BY handle_id;


-- combined query
-- selects all messages w/ their corresponding chat and handle info
-- removing duplicates and empty (attachment) messages
SELECT m.ROWID AS message_id, cmj.chat_id AS chat_id, m.handle_id AS handle_id,
text, is_from_me, style, group_id,
datetime((date/1000000000) + strftime('%s', '2001-01-01 00:00:00'), 'unixepoch', 'localtime') AS date,
h.id AS full_number, m.service AS service, person_centric_id AS person_id
FROM message AS m
INNER JOIN chat_message_join AS cmj
ON cmj.message_id = m.ROWID
INNER JOIN chat AS c
ON cmj.chat_id = c.ROWID
LEFT JOIN handle AS h
ON m.handle_id = h.ROWID
WHERE text IS NOT NULL
GROUP BY message_id;


-- select imessage/sms duplicates in chat_message_join
SELECT chat_id, message_id, COUNT(*)
FROM chat_message_join
GROUP BY message_id
HAVING COUNT(*) > 1;
