const state = {
  products: [],
  cart: JSON.parse(localStorage.getItem("bobaCart") || "{}"),
  category: "All"
};

const money = value => `Rs. ${value.toLocaleString("en-IN")}`;

function saveCart() {
  localStorage.setItem("bobaCart", JSON.stringify(state.cart));
}

async function loadProducts() {
  const response = await fetch("/api/products");
  state.products = await response.json();
  renderFilters();
  renderProducts();
  renderCart();
}

function renderFilters() {
  const categories = ["All", ...new Set(state.products.map(product => product.category))];
  document.getElementById("filters").innerHTML = categories.map(category => `
    <button class="filter ${state.category === category ? "active" : ""}" onclick="setCategory('${category}')">
      ${category}
    </button>
  `).join("");
}

function setCategory(category) {
  state.category = category;
  renderFilters();
  renderProducts();
}

function renderProducts() {
  const products = state.category === "All"
    ? state.products
    : state.products.filter(product => product.category === state.category);

  document.getElementById("products").innerHTML = products.map(product => `
    <article class="product ${product.id}">
      <div class="drink-art" aria-hidden="true"></div>
      <div class="product-body">
        <div class="meta">
          <span class="badge">${product.badge}</span>
          <span class="price">${money(product.price)}</span>
        </div>
        <h3>${product.name}</h3>
        <p>${product.description}</p>
        <div class="product-footer">
          <span>${product.category}</span>
          <button class="add" onclick="addToCart('${product.id}')">Add</button>
        </div>
      </div>
    </article>
  `).join("");
}

function addToCart(id) {
  state.cart[id] = (state.cart[id] || 0) + 1;
  saveCart();
  renderCart();
}

function changeQty(id, delta) {
  state.cart[id] = (state.cart[id] || 0) + delta;
  if (state.cart[id] <= 0) {
    delete state.cart[id];
  }
  saveCart();
  renderCart();
}

function getCartLines() {
  return Object.entries(state.cart)
    .map(([id, quantity]) => ({ product: state.products.find(item => item.id === id), quantity }))
    .filter(line => line.product);
}

function calculateTotals() {
  const subtotal = getCartLines().reduce((sum, line) => sum + line.product.price * line.quantity, 0);
  const packaging = subtotal ? 15 : 0;
  const delivery = subtotal && subtotal < 499 ? 35 : 0;
  return { subtotal, packaging, delivery, total: subtotal + packaging + delivery };
}

function renderCart() {
  const lines = getCartLines();
  const count = lines.reduce((sum, line) => sum + line.quantity, 0);
  const totals = calculateTotals();

  document.getElementById("cartCount").textContent = count;
  document.getElementById("subtotal").textContent = money(totals.subtotal);
  document.getElementById("packaging").textContent = money(totals.packaging);
  document.getElementById("delivery").textContent = money(totals.delivery);
  document.getElementById("total").textContent = money(totals.total);
  document.getElementById("checkoutButton").disabled = count === 0;

  document.getElementById("cartItems").innerHTML = lines.length ? lines.map(line => `
    <div class="cart-item">
      <div>
        <strong>${line.product.name}</strong>
        <span>${money(line.product.price)} x ${line.quantity}</span>
      </div>
      <div class="qty">
        <button type="button" onclick="changeQty('${line.product.id}', -1)">-</button>
        <b>${line.quantity}</b>
        <button type="button" onclick="changeQty('${line.product.id}', 1)">+</button>
      </div>
    </div>
  `).join("") : `<div class="empty">Your cart is empty. Add a drink to begin.</div>`;
}

document.getElementById("checkoutForm").addEventListener("submit", async event => {
  event.preventDefault();
  const formData = new FormData(event.currentTarget);
  const payload = {
    customer: Object.fromEntries(formData.entries()),
    items: Object.entries(state.cart).map(([id, quantity]) => ({ id, quantity }))
  };

  const response = await fetch("/api/orders", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  const result = await response.json();

  if (!response.ok) {
    alert(result.error || "Could not place order.");
    return;
  }

  state.cart = {};
  saveCart();
  renderCart();
  event.currentTarget.reset();

  const message = document.getElementById("message");
  message.style.display = "block";
  message.textContent = `Order ${result.order.id} placed. Total ${money(result.order.total)}. Estimated pickup/delivery: ${result.order.eta}.`;
});

loadProducts();
