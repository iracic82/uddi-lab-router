import { useState } from "react";
import axios from "axios";
import clsx from "clsx";

export default function App() {
  const [token, setToken] = useState("");
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await axios.post(
        "/resolve",
        { prompt },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setResult(res.data);
    } catch (e) {
      setError(e.response?.data?.detail || e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto mt-20">
      <h1 className="text-3xl font-bold mb-6 text-center">
        Instruqt Lab Router
      </h1>

      <label className="block mb-4">
        <span className="text-sm">API Token</span>
        <input
          className="w-full p-2 mt-1 rounded bg-slate-800 border border-slate-700"
          value={token}
          onChange={(e) => setToken(e.target.value)}
        />
      </label>

      <label className="block mb-4">
        <span className="text-sm">Prompt</span>
        <input
          className="w-full p-2 mt-1 rounded bg-slate-800 border border-slate-700"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
      </label>

      <button
        onClick={submit}
        disabled={loading}
        className={clsx(
          "w-full py-2 rounded font-semibold",
          loading
            ? "bg-slate-600 cursor-not-allowed"
            : "bg-blue-600 hover:bg-blue-700"
        )}
      >
        {loading ? "Thinking…" : "Get Invite"}
      </button>

      {result && (
        <p className="mt-6 text-green-400 break-all">
          Invite:{" "}
          <a
            href={result.invite_url}
            target="_blank"
            rel="noopener noreferrer"
            className="underline"
          >
            {result.invite_url}
          </a>
        </p>
      )}

      {error && (
        <p className="mt-6 text-red-400 whitespace-pre-line">{error}</p>
      )}
    </div>
  );
}
