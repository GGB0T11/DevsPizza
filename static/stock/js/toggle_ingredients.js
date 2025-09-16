document.addEventListener("DOMContentLoaded", function () {
  const typeChoice = document.getElementById("type");
  const ingredients = document.getElementById("ingredients");
  const quantity = document.getElementById("quantity");

  function toggleInputVisibility() {
    if (typeChoice.value === "food") {
      ingredients.style.display = "block";
      quantity.style.display = "none";
    } else {
      ingredients.style.display = "none";
      quantity.style.display = "block";
    }
  }

  toggleInputVisibility();

  typeChoice.addEventListener("change", toggleInputVisibility);
});
