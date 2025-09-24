import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult("");
  };

  const handleUpload = async () => {
    if (!file) {
      alert("파일을 선택해주세요.");
      return;
    }
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data.text || "텍스트가 없습니다.");
    } catch (err) {
      alert("에러 발생: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setResult("");
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>PDF 텍스트 변환기</h1>
      {!result && (
        <>
          <input type="file" accept=".pdf" onChange={handleFileChange} />
          <button onClick={handleUpload} disabled={loading}>
            {loading ? "처리중..." : "업로드 및 변환"}
          </button>
        </>
      )}
      {result && (
        <>
          <button onClick={handleReset}>뒤로</button>
          <pre style={{ whiteSpace: "pre-wrap", marginTop: 20 }}>{result}</pre>
        </>
      )}
    </div>
  );
}

export default App;