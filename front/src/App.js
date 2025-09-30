import React, { useState } from 'react';
import './App.css'; // CSS 파일을 불러옵니다.

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [convertedText, setConvertedText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setConvertedText(''); // 새 파일 선택 시 이전 텍스트 초기화
    setError('');
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('PDF 파일을 선택해주세요.');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      // 백엔드 API 엔드포인트로 변경해야 합니다.
      const response = await fetch('http://localhost:8000/upload/', { 
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json(); // 백엔드가 JSON 형태로 텍스트를 반환한다고 가정
      setConvertedText(data.text); // 백엔드 응답에서 텍스트 필드를 추출
    } catch (error) {
      console.error('Error uploading file:', error);
      setError('파일 업로드 및 변환 중 오류가 발생했습니다.');
      setConvertedText('');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>PDF 텍스트 변환기</h1>
      </header>
      <main className="App-main">
        <div className="upload-section">
          <input type="file" accept=".pdf" onChange={handleFileChange} />
          <button onClick={handleUpload} disabled={!selectedFile || loading}>
            {loading ? '변환 중...' : 'PDF 업로드 및 변환'}
          </button>
        </div>

        {error && <p className="error-message">{error}</p>}

        {convertedText && (
          <div className="text-container">
            <h2>변환된 텍스트:</h2>
            <div className="scrollable-text">
              <pre>{convertedText}</pre>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;