import React, { useState } from 'react';

function HoroscopePrediction() {
    const [name, setName] = useState('');
    const [day, setDay] = useState('');
    const [month, setMonth] = useState('');
    const [year, setYear] = useState('');
    const [yearToCheck, setYearToCheck] = useState('');
    const [prediction, setPrediction] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const birthday = `${year}-${month}-${day}`;
        const response = await fetch('/predict', {
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
                    <div className="flex space-x-2">
                        <input
                            type="number"
                            placeholder="Ngày"
                            value={day}
                            onChange={(e) => setDay(e.target.value)}
                            className="w-1/3 px-3 py-2 border rounded"
                            required
                        />
                        <input
                            type="number"
                            placeholder="Tháng"
                            value={month}
                            onChange={(e) => setMonth(e.target.value)}
                            className="w-1/3 px-3 py-2 border rounded"
                            required
                        />
                        <input
                            type="number"
                            placeholder="Năm"
                            value={year}
                            onChange={(e) => setYear(e.target.value)}
                            className="w-1/3 px-3 py-2 border rounded"
                            required
                        />
                    </div>
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
                {prediction && <p className="mt-4 text-center">{prediction}</p>}
            </form>
        </div>
    );
}

export default HoroscopePrediction;