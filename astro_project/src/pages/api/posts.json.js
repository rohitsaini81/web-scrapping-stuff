export async function GET() {
  const response = await fetch("http://localhost:8000/api/apps");
  const data = await response.json();

  return new Response(JSON.stringify(data), {
    headers: { "Content-Type": "application/json" },
  });
}
