document.addEventListener("DOMContentLoaded", function () {
  const transactionType = document.getElementById("transaction-type");
  const productSelect = document.getElementById("product-select");
  const ingredientSelect = document.getElementById("ingredient-select");

  function toggleInputVisibility() {
    if (transactionType.value === "inflow") {
      ingredientSelect.style.display = "block";
      productSelect.style.display = "none";
    } else {
      ingredientSelect.style.display = "none";
      productSelect.style.display = "block";
    }
  }

  toggleInputVisibility();

  transactionType.addEventListener("change", toggleInputVisibility);
});
