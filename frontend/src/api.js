export async function schedule(algorithm, processes, quantum = null) {
  const payload = { algorithm, processes };
  if (algorithm === "RR") payload.quantum = quantum;

  const res = await fetch("http://localhost:5001/api/schedule", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }

  return res.json();
}
