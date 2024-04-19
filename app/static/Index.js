// scripts for 'index.html' go here

function CarouselCardSlider() {
  //NOTE: causes is a global variable defined in a script tag in index.html

  // State for the active card
  const [activeIndex, setActiveIndex] = React.useState(0);

  const goPrev = () => {
    setActiveIndex((prevIndex) =>
      prevIndex - 1 >= 0 ? prevIndex - 1 : causes.length - 1,
    );
  };

  const goNext = () => {
    setActiveIndex((prevIndex) =>
      prevIndex + 1 < causes.length ? prevIndex + 1 : 0,
    );
  };
  const handleDonate = (causeId) => {
    const data = { cause_id: causeId };
    const data_json = JSON.stringify(data);
    fetch("/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: data_json,
    })
      .then((response) => response.text())
      .then((htmlString) => {
        // Replace the content of the entire body with the received HTML string
        document.body.innerHTML = htmlString;
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <div className="slider-container">
      x
      <div className="slider-wrapper">
        {causes.map((cause, index) => (
          <div
            key={cause.id}
            className={`card ${index === activeIndex ? "active" : ""}`}
          >
            {cause.img_url && (<img src={cause.imageUrl}/>)}
            <h3>{cause.name}</h3>
            <p>{cause.description}</p>
            <p>Current amount: {cause.current_amount}</p>
            <p>Goal amount: {cause.goal_amount}</p>
            <button onClick={() => handleDonate(cause.id)}>DONATE</button>
          </div>
        ))}
      </div>
      <button className="prev" onClick={goPrev}>
        &lt;
      </button>
      <button className="next" onClick={goNext}>
        &gt;
      </button>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("react-root")).render(
  <CarouselCardSlider />,
);
