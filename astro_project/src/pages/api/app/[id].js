export const prerender = false;

export async function GET({ params }) {
  const { id } = params;

  const response = await fetch(`http://localhost:5000/api/app/${id}`);
  const data = await response.json();

  return new Response(JSON.stringify(data), {
    headers: { "Content-Type": "application/json" },
  });
}
