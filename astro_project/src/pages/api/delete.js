import { deletePost } from "../../data/posts.js";

export async function post({ request }) {
  const data = await request.json();
  deletePost(data.id);
  return new Response(JSON.stringify({ success: true }));
}
