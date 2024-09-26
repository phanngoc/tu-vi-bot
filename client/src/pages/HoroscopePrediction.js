import React, { useState } from 'react';

const HoroscopePrediction = () => {
    const [name, setName] = useState('');
    const [birthday, setBirthday] = useState('');
    const [yearToCheck, setYearToCheck] = useState('');
    const [prediction, setPrediction] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ birthday, yearToCheck }),
        });
        const data = await response.json();
        setPrediction(data.message);
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow-md w-full max-w-sm">
                <h2 className="text-2xl font-bold mb-4">Nhập thông tin của bạn để dự đoán tử vi</h2>
                <div className="mb-4">
                    <label className="block text-gray-700">Tên:</label>
                    <input
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        className="w-full px-3 py-2 border rounded"
                        required
                    />
                </div>
                <div className="mb-4">
                    <label className="block text-gray-700">Ngày sinh:</label>
                    <input
                        type="date"
                        value={birthday}
                        onChange={(e) => setBirthday(e.target.value)}
                        className="w-full px-3 py-2 border rounded"
                        required
                    />
                </div>
                <div className="mb-4">
                    <label className="block text-gray-700">Năm cần xem:</label>
                    <input
                        type="number"
                        value={yearToCheck}
                        onChange={(e) => setYearToCheck(e.target.value)}
                        className="w-full px-3 py-2 border rounded"
                        required
                    />
                </div>
                <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">
                    Dự đoán
                </button>
                {prediction && <p className="mt-4 text-green-500">{prediction}</p>}
            </form>
        </div>
    );
};

export default HoroscopePrediction;