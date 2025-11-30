// db.js
import pkg from 'pg';
const { Pool } = pkg;


import dotenv from 'dotenv';
dotenv.config();
const connectionString = process.env.POSTGRES;

if (!connectionString) {
  throw new Error("DATABASE_URL is not defined in environment variables");
}




// const connectionString = process.env.DATABASE_URL
//  'postgres://rohitsaini:mypassword@localhost:5432/mydatabase';

const pool = new Pool({
  connectionString:connectionString,
});

console.log(connectionString)

export default pool;




export async function fetchApps(tableName) {
  try {
    console.log("heyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
    const result = await pool.query(`SELECT * FROM ${tableName}`);
    return result.rows; 
  } catch (err) {
    console.error('Error fetching blogs:', err);
    throw err;
  }
}



export async function fetchBlogPost(slug) {
  try {
    const decodedSlug = decodeURIComponent(slug); // 🔥 important
    const result = await pool.query(
      'SELECT * FROM blogs WHERE title = $1',
      [decodedSlug]
    );
    return result.rows[0]; 
  } catch (err) {
    console.error('Error fetching blogs:', err);
    throw err;
  }
}







export async function fetchBlogPostContent(blog_id) {
  try {
    // console.log(blog_id)
    const result = await pool.query(
      'SELECT * FROM blog_posts WHERE blog_id = $1',
      [blog_id]
    );
    return result.rows[0]; 
  } catch (err) {
    console.error('Error fetching blogs:', err);
    throw err;
  }
}