import React from 'react';
import Slider from './Slider';
import DeveloperCard from './DeveloperCard';

const Home = () => {
  return (
    <div>
      {/* Slider Section */}
      <Slider />

      {/* Developer Section */}
      <section className="developer-section">
        <h2>Meet the Developer</h2> {/* Heading before the developer card */}
        <DeveloperCard
          name="Haider Karar"
          description="Hi! I’m Haider, a passionate Python developer and AI student at ITU Lahore. 
          I specialize in data visualization, machine learning, and building dynamic web applications."
          skills={['Python', 'Flask', 'React', 'Streamlit', 'Machine Learning']}
          image="https://via.placeholder.com/150" // Replace with your photo URL if available
        />
      </section>
    </div>
  );
};

export default Home;
