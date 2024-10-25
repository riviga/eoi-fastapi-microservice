import React, { useEffect } from "react";
import Wrapper from "./Wrapper";

type OrderType = {
  id: string;
  product_id: number;
  quantity: number;
  price: number;
  fee: number;
  total: number;
  status: string;
};


export const Orders = () => { // writing tsx
  const [products, setOrders] = React.useState<OrderType[]>([]);

  useEffect(() => {
    (async () => {
      const response = await fetch("/app/pedidos");
      const content = await response.json();
      setOrders(content);
    })();
  }, []);

  return (
    <Wrapper>
      <div className="table-responsive small">
        <table className="table table-striped table-sm">
          <thead>
            <tr>
              <th scope="col">Order ID</th>
              <th scope="col">Product ID</th>
              <th scope="col">Quantity</th>
              <th scope="col">Price</th>
              <th scope="col">Fee</th>
              <th scope="col">Total</th>
              <th scope="col">Status</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => {
              return (
                <tr key={product.id}>
                  <td>{product.id}</td>
                  <td>{product.product_id}</td>
                  <td>{product.quantity}</td>
                  <td>{product.price}</td>
                  <td>{product.fee}</td>
                  <td>{product.total}</td>
                  <td>{product.status}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </Wrapper>
  );
};
