import { addPost } from "../../data/posts.js";

export async function post({ request }) {
  const data = await request.json();
  addPost(data.title, data.content);
  return new Response(JSON.stringify({ success: true }));
}
