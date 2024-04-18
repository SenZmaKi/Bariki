// scripts for 'index.html' go here

function CarouselCardSlider() {
    // Dummy data for the carousel
    const cards = [
        { id: 1, name: 'David Dell', description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.', imageUrl: 'path-to-image' },
        { id: 2, name: 'Rose Bush', description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.', imageUrl: 'path-to-image' },
        { id: 3, name: 'Jones Gail', description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.', imageUrl: 'path-to-image' }
    ];

    // State for the active card
    const [activeIndex, setActiveIndex] = React.useState(0);

    const goPrev = () => {
        setActiveIndex((prevIndex) => prevIndex - 1 >= 0 ? prevIndex - 1 : cards.length - 1);
    };

    const goNext = () => {
        setActiveIndex((prevIndex) => prevIndex + 1 < cards.length ? prevIndex + 1 : 0);
    };

    return (
        <div className="slider-container">x
            <div className="slider-wrapper">
                {cards.map((card, index) => (
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