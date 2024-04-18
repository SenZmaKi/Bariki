// scripts for 'index.html' go here


function CarouselCardSlider() {
    //NOTE: causes is a global variable defined in a script tag in index.html
 
    // State for the active card
    const [activeIndex, setActiveIndex] = React.useState(0);

    const goPrev = () => {
        setActiveIndex((prevIndex) => prevIndex - 1 >= 0 ? prevIndex - 1 : causes.length - 1);
    };

    const goNext = () => {
        setActiveIndex((prevIndex) => prevIndex + 1 < causes.length ? prevIndex + 1 : 0);
    };

    return (
        <div className="slider-container">x
            <div className="slider-wrapper">
                {causes.map((card, index) => (
                    <div key={card.id} className={`card ${index === activeIndex ? 'active' : ''}`}>
                        <img src={card.imageUrl} alt={card.name} />
                        <h3>{card.name}</h3>
                        <p>{card.description}</p>
                        <button>DONATE</button>
                    </div>
                ))}
            </div>
            <button className="prev" onClick={goPrev}>&lt;</button>
            <button className="next" onClick={goNext}>&gt;</button>
        </div>
    );
}

ReactDOM.createRoot(document.getElementById('react-root')).render(<CarouselCardSlider />);
