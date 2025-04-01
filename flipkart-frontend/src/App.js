import React, { useState } from 'react';
import './styles.css';

function App() {
    const [review, setReview] = useState('');
    const [response, setResponse] = useState('');

    const handleSubmit = async () => {
        try {
            const res = await fetch('http://localhost:5000/reviews', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ content: review }),
            });
            const data = await res.json();

            // Format the response without brackets and inverted commas
            const formattedResponse = `
Fake: ${data.fake}
Keywords: ${data.keywords.join(', ')}
Language: ${data.language}
Rating: ${data.rating}
Review: ${data.review}
Sentiment: ${data.sentiment}
Translation: ${data.translation}
            `;

            setResponse(formattedResponse);
        } catch (error) {
            console.error('Error:', error);
            setResponse('Error submitting review');
        }
    };

    return (
        <div className="container">
            <h1>Flipkart Review Sentiment Analysis</h1>
            <textarea
                placeholder="Enter your review..."
                value={review}
                onChange={(e) => setReview(e.target.value)}
            ></textarea>
            <button onClick={handleSubmit}>Submit Review</button>
            <pre>{response}</pre>
        </div>
    );
}

export default App;
