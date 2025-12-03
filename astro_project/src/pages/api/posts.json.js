import { posts } from "../../data/posts.js";

export async function get() {
  return new Response(JSON.stringify(posts), {
    headers: { "Content-Type": "application/json" },
  });
}
