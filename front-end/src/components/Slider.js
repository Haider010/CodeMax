import React from 'react';
import './styles/Slider.css'; // Add custom CSS for styling the slider

const Slider = () => {
  return (
    <div className="slider">
      <div className="slide">
        <h2>Welcome to CodeMax</h2>
        <p>Your journey to coding excellence starts here!</p>
      </div>
      <div className="slide">
        <h2>Study Material</h2> {/* Updated slide */}
        <p>Access a wide range of study materials to boost your knowledge.</p>
      </div>
      <div className="slide">
        <h2>Challenging Problems</h2>
        <p>Enhance your skills by solving real-world problems.</p>
      </div>
    </div>
  );
};

export default Slider;
