const form = document.getElementById("predict-form");
const resultDiv = document.getElementById("result");

form.addEventListener("submit", async function (e) {
  e.preventDefault();

  // Get raw input values and convert them
  const bedrooms = parseInt(document.getElementById("bedrooms").value);
  const bathrooms = parseInt(document.getElementById("bathrooms").value);
  const sqft = parseFloat(document.getElementById("sqft").value);
  const future_year = parseInt(document.getElementById("future_year").value);

  // FormData sends data as string, so do manual appending
  const formData = new FormData();
  formData.append("bedrooms", bedrooms);
  formData.append("bathrooms", bathrooms);
  formData.append("sqft", sqft);
  formData.append("future_year", future_year);

  try {
    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      resultDiv.innerHTML = `<p style="color: red;">Error: ${errorData.detail}</p>`;
      return;
    }

    const data = await response.json();
    resultDiv.innerHTML = `<h3>Predicted Price: ₹ ${data.predicted_price.toLocaleString('en-IN')}</h3>`;
  } catch (error) {
    resultDiv.innerHTML = `<p style="color: red;">Error predicting price. Make sure the backend is running.</p>`;
    console.error("Prediction error:", error);
  }
});
