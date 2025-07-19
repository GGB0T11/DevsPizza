document.addEventListener("DOMContentLoaded", function () {
  const transactionType = document.getElementById("transaction-type");
  const productSelect = document.getElementById("product-select");
  const productAmount = document.getElementById("product-amount");
  const ingredientSelect = document.getElementById("ingredient-select");

  function toggleInputVisibility() {
    if (transactionType.value === "inflow") {
      productSelect.style.display = "none";
      productAmount.style.display = "none";
      ingredientSelect.style.display = "block";
    } else {
      productSelect.style.display = "block";
      productAmount.style.display = "block";
      ingredientSelect.style.display = "none";
    }
  }

  toggleInputVisibility();

  transactionType.addEventListener("change", toggleInputVisibility);
});
