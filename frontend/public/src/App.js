import React, { useState } from "react";
import './App.css';
import bookIcon from './book-icon.jpg';

function App() {
  const [form, setForm] = useState({
    age: "",
    lesson: "",
    topic: "",
    hero: "",
    characteristics: ""
  });
  const [textResponse, setTextResponse] = useState("");

  function handleChange(e) {
    const { name, value } = e.target;
    setForm(prevForm => ({ ...prevForm, [name]: value }));
  }

  function renderStoryContent() {
    if (!textResponse || !textResponse.content) {
      return null;
    }

    return (
      <div className="story-container">
        <h2 className="story-title">{textResponse.title}</h2>
        {textResponse.content.map((item, index) => (
          <div key={index} className="story-page">
            <p className="story-paragraph">{item.paragraph}</p>
            <p className="story-prompt">/imagine {item.image_prompt}</p>
            <p className="story-caption">[{item.image_caption}]</p>

          </div>
        ))}
        <br></br>
        <hr></hr>
        <br></br>
          <div className="story-page">
            {Object.keys(textResponse.descriptions).map(key => (
            <p className="story-caption">{key}: {textResponse.descriptions[key]}</p>
            ))}
        </div>
        
      </div>
    );
  }

  function handleSubmit(e) {
    e.preventDefault();
    fetch(`${process.env.REACT_APP_API_BASE_URL}/generate-book`, {
      method: "POST",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(form),
    })
    .then((res) => res.json())
    .then((data) => {
      setTextResponse(data.response)
    })
    .catch((err) => {
      console.log(err);
    });
  }

  return (
    <div className="container">
      <header className="header">
        <img src={bookIcon} className="logo" alt="book icon" />
        <h1 className="title">
          Little Legend Lab
        </h1>
        <p>
          Welcome to the most personalized story book generator for the new generation.
        </p>
        <form onSubmit={handleSubmit}>
          <div className="form-section">
            <div className="dropdowns">
              <div className="dropdown-row">
                <div className="dropdown-label">
                  What is the age of your listener?
                </div>
                <input 
                  list="ageOptions" 
                  className="dropdown" 
                  name="age" 
                  id="age" 
                  placeholder="Select or type an age" 
                  value={form.age}
                  onChange={handleChange} />                
              <datalist id="ageOptions">
                  <option value="4" />
                  <option value="5" />
                  <option value="6" />
                  <option value="7" />
                  <option value="8" />
                  <option value="9" />
                  <option value="10" />
                  <option value="11" />
                  <option value="12" />
                  <option value="13" />
                  <option value="14" />
                  <option value="15" />
                  <option value="16" />
                  <option value="17" />
                  <option value="18" />
                  {/* Add more age options as needed */}
                </datalist>
              </div>
              <div className="dropdown-row">
                <div className="dropdown-label">
                  Select Lesson
                </div>
                <input list="lessonOptions" value={form.lesson}
                  onChange={handleChange} className="dropdown" name="lesson" id="lesson" placeholder="Select or type a lesson" />
                <datalist id="lessonOptions">
                  <option value="Alphabet" />
                  <option value="Numbers" />
                  <option value="Colors" />
                  {/* Add more lesson options as needed */}
                </datalist>
              </div>
              <div className="dropdown-row">
                <div className="dropdown-label">
                  Topic of the story
                </div>
                <input list="topicOptions" value={form.topic}
                  onChange={handleChange} className="dropdown" lassName="dropdown" name="topic" id="topic" placeholder="Select or type a topic" />
                <datalist id="topicOptions">
                  <option value="Adventure" />
                  <option value="Fantasy" />
                  <option value="Mystery" />
                  {/* Add more topic options as needed */}
                </datalist>
              </div>
              <h2 className="subtitle">Legend Questions</h2>
              <div className="dropdown-row">
                <div className="dropdown-label">
                  If you'd like the listener of the story to be the hero, what is his/her name?
                </div>
                <input list="heroOptions" value={form.hero}
                  onChange={handleChange} className="dropdown" name="hero" id="hero" placeholder="Select or type a response" />
                <datalist id="heroOptions">
                  <option value="Adam" />
                  <option value="Haley" />
                </datalist>
              </div>
              <div className="dropdown-row">
                <div className="dropdown-label">
                  What are some characteristics of your listener?
                </div>
                <input list="characteristicsOptions" value={form.characteristics}
                  onChange={handleChange} className="dropdown" name="characteristics" id="characteristics" placeholder="Select or type characteristics" />
                <datalist id="characteristicsOptions">
                  <option value="Brave" />
                  <option value="Curious" />
                  <option value="Kind" />
                  {/* Add more characteristic options as needed */}
                </datalist>
              </div>
              <button className="submit-button">Submit</button>
                {renderStoryContent()}
            </div>
          </div>
        </form>
        <a
          className="link"
          href="https://beagoodbot.com"
          target="_blank"
          rel="noopener noreferrer"
        >
          Be A Good Bot - AI Club
        </a>
      </header>



    </div>
  );
}

export default App;
