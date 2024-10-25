import Products from "./components/products";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ProductsCreate } from "./components/ProductsCreate";
import { NewOrder } from "./components/NewOrder";
import { Orders } from "./components/Orders";
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Products />} />
        <Route path="/create" element={<ProductsCreate />} />
        <Route path="/new_order" element={<NewOrder />} />
        <Route path="/orders" element={<Orders />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
