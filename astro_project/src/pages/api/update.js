import { updatePost } from "../../data/posts.js";

export async function post({ request }) {
  const data = await request.json();
  updatePost(data.id, data.title, data.content);
  return new Response(JSON.stringify({ success: true }));
}
