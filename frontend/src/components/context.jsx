import React, { useState, useEffect } from 'react';

const Context = () => {
    /**
     * - show previously collected context about the user
     * - allow the user to add new context
     */
    const [context, setContext] = useState([]); // history of context
    const [newContext, setNewContext] = useState(''); // new context added by user
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    //  initialize context from memory 
    useEffect(() => {
        const fetchContext = async () => {
            try {
                setLoading(true);
                setError(null);
                const response = await fetch('http://localhost:8000/get_context', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                // set context to the context array fetched from the backend
                setContext(Array.isArray(data.contexts) ? data.contexts : []);
                console.log("context:", data.contexts);
            } catch (error) {
                console.error('Error fetching context:', error);
                setError('Failed to load context. Please try again later.');
                setContext([]);
            } finally {
                setLoading(false);
            }
        };
        fetchContext();
    }, []);

    // add new context to memory
    const addContext = async (text) => {
        if (!text.trim()) return;
        
        try {
            const response = await fetch('http://localhost:8000/add_context', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    text: text,
                    category: "Unknown"  // Add default category
                }),
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const newContextItem = await response.json();
            if (newContextItem.status === 'error') {
                throw new Error(newContextItem.message);
            }
            setContext([...context, newContextItem]);
            setNewContext(''); // Clear input after successful add
        } catch (error) {
            console.error('Error adding context:', error);
            alert('Failed to add context: ' + error.message);
        }
    };
    
    if (loading) return <div>Loading context...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div>
            <h1>Context</h1>
            <div className="context-list">
                {context.map((item, index) => (
                    <div key={index} className="context-item">
                        <span className="category">{item.category}</span>
                        <p className="text">{item.text}</p>
                    </div>
                ))}
            </div>
            <div className="add-context">
                <input
                    type="text"
                    value={newContext}
                    onChange={(e) => setNewContext(e.target.value)}
                    placeholder="Add new context"
                />
                <button onClick={() => addContext(newContext)}>Add</button>
            </div>
            
        </div>
    );
};

export default Context;