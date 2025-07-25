# Database (Firestore) Structure

With the transition to Firebase, the following Firestore collection structure is proposed to replace the existing:

// Firestore構造（構造定義の記述）

Collection: users
├── Document ID: <line_user_id>
    ├── name: string        // 例: "山田太郎"
    ├── mode: string        // 例: "first"

Collection: [gameId]
├── Document ID: <line_user_id>
    ├── start: int        // timestamp
    ├── end: int        // 例: timestamp
    ├── score: int        // 例: end - start
    ├── title: string        // 例: gemeId

The project is organized into several directories, each with a specific responsibility: