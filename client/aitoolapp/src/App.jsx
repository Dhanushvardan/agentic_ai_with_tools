import { useState } from "react";
import "./App.scss";
import axios from "axios";

function App() {
  const [inval, setInVal] = useState("");
  const [inval1, setInVal1] = useState(0);
  const [inval2, setInVal2] = useState("");
  const [resp, setResp] = useState("");
  const checkCon = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/");
      console.log(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  const triggerdb = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/adduser", {
        id: 0,
        bio: inval,
      });
      console.log(res.data.response);
    } catch (err) {
      console.log(err);
    }
  };
  const checkdb = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/getdata");
      console.log(res.data.response);
    } catch (err) {
      console.log(err);
    }
  };
  const askai = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/askai", {
        msg: inval,
      });
      console.log(res.data.response);
      setResp(res.data.response);
    } catch (err) {
      console.log(err);
    }
  };
  return (
    <div className="App">
      <div className="header">Hello agentic ai with db</div>
      <div className="body">
        <label>Ask ai</label>
        <input
          onChange={(e) => {
            setInVal(e.target.value);
          }}
        ></input>

        <button onClick={checkCon}>check connection</button>
        {/* <button onClick={triggerdb}>send to PYMONGO</button> */}
        <button onClick={checkdb}>check db</button>
        <button onClick={askai}>ask ai</button>
      </div>
      <div className="footer">{resp}</div>
    </div>
  );
}

export default App;
