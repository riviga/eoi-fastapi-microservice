import { useEffect, useState } from "react";
import Wrapper from "./Wrapper";

export const NewOrder = () => {
  const [product_id, setId] = useState("");
  const [quantity, setQuantity] = useState("");
  const [message, setMessage] = useState("Place your order");

  useEffect(() => {
    (async () => {
      try {
        if (product_id) {
          const response = await fetch(`/api/farmacos/${product_id}`);
          const content = await response.json();
          if(content.name!= undefined){
            const price = parseFloat(content.price) * 1.05;
            setMessage(`The price of ${content.name} is €${price}`);
          }
          else{
            setMessage(`Invalid product ID`);
          }          
        }
      } catch (error) {
        setMessage("Product not found");
      }
    })();
  }, [product_id]);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    await fetch("/app/pedidos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        product_id,
        quantity,
      }),
    });

    setMessage("Your order has been placed");
  };

  return (
    <Wrapper>
      <div className="container">
        <main>
          <div className="py-5 text-center">
            <h2>New order form</h2>
            <p className="lead">{message}</p>
          </div>
          <form onSubmit={submit}>
            <div className="row g-3">
              <div className="col-sm-6">
                <label className="form-label">Product ID</label>
                <input
                  className="form-control"
                  type="text"
                  placeholder="Product"
                  aria-label="Product"
                  onChange={(e) => setId(e.target.value)}
                />
              </div>
              <div className="col-sm-6">
                <label className="form-label">Quantity</label>
                <input
                  type="number"
                  className="form-control"
                  placeholder="Quantity"
                  aria-label="Quantity"
                  onChange={(e) => setQuantity(e.target.value)}
                />
              </div>
            </div>
            <hr className="my-4" />
            <button className="w-100 btn btn-primary btn-lg" type="submit">
              Buy
            </button>
          </form>
        </main>
      </div>
    </Wrapper>
  );  
};
