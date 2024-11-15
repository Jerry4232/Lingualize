-- schema.sql


CREATE TABLE user (
    user_id INTEGER NOT NULL PRIMARY KEY,
    -- Note: this length check might not work properly
    username TEXT NOT NULL UNIQUE CHECK ( LENGTH(password) > 0 ),
    password TEXT NOT NULL CHECK ( LENGTH(password) >= 6 ),

    email TEXT,
    profile_picture_url TEXT,
    creation_timestamp TEXT NOT NULL,
    update_timestamp TEXT NOT NULL,
    proficiency_rating INTEGER
) STRICT;


CREATE TABLE scene (
    -- fixed after development
    -- ex. coffee shop
    scene_id INTEGER NOT NULL PRIMARY KEY,
    description TEXT NOT NULL UNIQUE,
    scene_file_path TEXT NOT NULL
) STRICT;


CREATE TABLE role (
    -- fixed after development
    -- generated sound from api
    role_id INTEGER NOT NULL PRIMARY KEY,
    gender TEXT NOT NULL,
    -- category might be more specific
    category TEXT NOT NULL,
    api_id TEXT NOT NULL
) STRICT;


CREATE TABLE user_scene (
    -- user's scene
    -- ex. user entering coffee shop
    -- but the user does not have one role yet (no conversation)
    user_scene_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    scene_id INTEGER NOT NULL,
     -- Ensures each scene can appear only once per user
    --  UNIQUE (user_id, scene_id),
    -- default in PST (UTC-8), time when enter scene
    creation_timestamp TEXT NOT NULL,
    update_timestamp TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (scene_id) REFERENCES scene(scene_id)
);


CREATE TABLE catalog (
    -- user's specific role in one scene
    -- ex. a customer in the coffee shop
    catalog_id INTEGER PRIMARY KEY,
    user_scene_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    -- default in PST (UTC-8), time when choosing role
    creation_timestamp TEXT NOT NULL,
    update_timestamp TEXT NOT NULL,
    FOREIGN KEY (user_scene_id) REFERENCES user_scene(user_scene_id),
    FOREIGN KEY (role_id) REFERENCES role(role_id)
);


CREATE TABLE message (
    message_id INTEGER NOT NULL PRIMARY KEY,
    catalog_id INTEGER NOT NULL,
    -- speaker should be user or AI(with specific role)
    speaker TEXT NOT NULL,
    -- respond from usr/chatgpt
    message_text TEXT NOT NULL,
    -- respond from usr/elevenlab
    audio_file_path TEXT NOT NULL,
    -- respond from sampling,
    -- null if this message is from AI
    corrected_message_text TEXT,
    -- Note: this timestamp may differ
    --  between user interface and server receives message
    creation_timestamp TEXT NOT NULL,
    foreign key (catalog_id) REFERENCES catalog(catalog_id)
) STRICT;


CREATE TABLE grammar_error (
    grammar_error_id INTEGER NOT NULL PRIMARY KEY,
    message_id INTEGER NOT NULL,
    -- minor or major error
    severity TEXT NOT NULL,
    type TEXT NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (message_id) REFERENCES message (message_id)
) STRICT;


CREATE TABLE pronunciation (
    pronunciation_id INTEGER NOT NULL PRIMARY KEY,
    overall_rating INTEGER NOT NULL,
    message_id INTEGER NOT NULL,
    FOREIGN KEY (message_id) REFERENCES message (message_id)
) STRICT;
