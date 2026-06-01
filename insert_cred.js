const crypto = require('crypto');
const sqlite3Path = '/usr/local/lib/node_modules/n8n/node_modules/.pnpm/sqlite3@5.1.7/node_modules/sqlite3';
const sqlite3 = require(sqlite3Path);

const ENCRYPTION_KEY = 'dNr4Ns9Fd1uUtSWD5BaL2qBa9f5bxbDd';
const DB_PATH = '/home/node/.n8n/database.sqlite';

function encrypt(text, key) {
    const keyBuffer = Buffer.alloc(32);
    Buffer.from(key).copy(keyBuffer);
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-cbc', keyBuffer, iv);
    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return iv.toString('hex') + ':' + encrypted;
}

const smtpData = {
    host: process.env.SMTP_HOST || 'smtp.example.com',
    port: Number(process.env.SMTP_PORT || 465),
    user: process.env.SMTP_USER || 'your-email@example.com',
    password: process.env.SMTP_PASSWORD || 'replace-with-secret',
    ssl: true,
    allowUnauthorizedCerts: false
};

const encrypted = encrypt(JSON.stringify(smtpData), ENCRYPTION_KEY);
const now = new Date().toISOString();

const db = new sqlite3.Database(DB_PATH, (err) => {
    if (err) { console.error('DB open error:', err.message); process.exit(1); }
    console.log('DB opened');
});

// First check the schema
db.all("SELECT sql FROM sqlite_master WHERE type='table' AND name LIKE '%credential%'", [], (err, rows) => {
    if (err) { console.error('Schema error:', err.message); return; }
    rows.forEach(r => console.log('Schema:', r.sql));
    
    // Try to get existing credentials to understand structure
    db.all("SELECT id, name, type FROM credentials_entity LIMIT 5", [], (err2, rows2) => {
        if (err2) { console.log('Select error:', err2.message); }
        else { console.log('Existing creds:', JSON.stringify(rows2)); }
        
        // Insert SMTP credential with id that matches what the workflow expects
        const insertSql = `INSERT OR REPLACE INTO credentials_entity 
            (id, name, data, type, nodesAccess, createdAt, updatedAt) 
            VALUES (?, ?, ?, ?, ?, ?, ?)`;
        
        db.run(insertSql, [
            'smtp-credentials-id',
            'SMTP account',
            encrypted,
            'smtp',
            JSON.stringify([]),
            now,
            now
        ], function(err3) {
            if (err3) {
                console.error('Insert error:', err3.message);
                // Try without nodesAccess
                const insertSql2 = `INSERT OR REPLACE INTO credentials_entity 
                    (id, name, data, type, createdAt, updatedAt) 
                    VALUES (?, ?, ?, ?, ?, ?)`;
                db.run(insertSql2, ['smtp-credentials-id','SMTP account',encrypted,'smtp',now,now], function(e2) {
                    if (e2) console.error('Insert2 error:', e2.message);
                    else console.log('SUCCESS (without nodesAccess) - rows changed:', this.changes);
                    db.close();
                });
            } else {
                console.log('SUCCESS - rows changed:', this.changes);
                db.close();
            }
        });
    });
});
