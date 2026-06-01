const sqlite3Path = '/usr/local/lib/node_modules/n8n/node_modules/.pnpm/sqlite3@5.1.7/node_modules/sqlite3';
const sqlite3 = require(sqlite3Path);
const DB_PATH = '/home/node/.n8n/database.sqlite';

const db = new sqlite3.Database(DB_PATH);

const projectId = process.env.N8N_PROJECT_ID;

const linkCredential = (targetProjectId) => {
    const now = new Date().toISOString();
    db.run(
        `INSERT OR REPLACE INTO shared_credentials (credentialsId, projectId, role, createdAt, updatedAt) VALUES (?, ?, ?, ?, ?)`,
        ['smtp-credentials-id', targetProjectId, 'credential:owner', now, now],
        function(err2) {
            if (err2) console.error('shared_credentials error:', err2.message);
            else console.log('shared_credentials link created - rows:', this.changes);

            db.all("SELECT id, name, type FROM credentials_entity", [], (e3, rows) => {
                console.log('All credentials:', JSON.stringify(rows));
                db.close();
            });
        }
    );
};

if (projectId) {
    linkCredential(projectId);
} else {
    db.get("SELECT id, type, name FROM project LIMIT 1", [], (err, project) => {
    if (err || !project) {
        console.log('Project error:', err ? err.message : 'no project found');
        db.close();
        return;
    }
    console.log('Using project ID:', project.id);
    linkCredential(project.id);
});
}
