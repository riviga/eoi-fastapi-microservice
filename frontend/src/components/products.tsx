import React, { useEffect } from "react";
import { Link } from "react-router-dom";
import Wrapper from "./Wrapper";

type ProductType = {
  id: number;
  name: string;
  price: number;
  quantity: number;
  Actions: string;
};

const Products = () => {
  // writing tsx
  const [products, setProducts] = React.useState<ProductType[]>([]);

  useEffect(() => {
    (async () => {
      const response = await fetch("/api/farmacos");
      const content = await response.json();
      setProducts(content);
    })();
  }, []);

  const del = async (id: number) => {
    if (window.confirm("Are you sure you want to delete this product?")) {
      await fetch(`/api/farmacos/${id}`, {
        method: "DELETE",
      });

      setProducts(products.filter((p) => p.id !== id));
    }
  };

  return (
    <Wrapper>
      <div className="pt-3 pb-2 mb-3 border-bottom">
        <Link to={"/create"} className="btn btn-sm btn-outline-secondary">
          {" "}
          Add{" "}
        </Link>
      </div>
      <div className="table-responsive small">
        <table className="table table-striped table-sm">
          <thead>
            <tr>
              <th scope="col">ID</th>
              <th scope="col">Name</th>
              <th scope="col">Price</th>
              <th scope="col">Quantity</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => {
              return (
                <tr key={product.id}>
                  <td>{product.id}</td>
                  <td>{product.name}</td>
                  <td>{product.price}</td>
                  <td>{product.quantity}</td>
                  <td>
                    <a
                      href="#"
                      className="btn btn-outline-secondary btn-sm"
                      onClick={() => del(product.id)}
                    >
                      Delete
                    </a>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </Wrapper>
  );
};

export default Products;
