SELECT
    cmj.chat_id AS chat_id,
    message_id,
    chj.handle_id AS handle_id,
    message_date AS date,
    m.text AS text,
    m.is_from_me
FROM chat_message_join AS cmj
    INNER JOIN message AS m
        ON cmj.message_id = m.ROWID
    INNER JOIN chat_handle_join AS chj
        ON cmj.chat_id = chj.chat_id
ORDER BY chj.handle_id DESC
LIMIT 1;