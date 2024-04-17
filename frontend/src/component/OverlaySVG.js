import React from "react";
import { ReactComponent as Cardback } from "../Cardback.svg";
import { ReactComponent as ImageMask } from "../ImageMask.svg";
import { ReactComponent as TextFields } from "../TextFields.svg";
import { useState } from "react";
import LargeModal from "./LargeModal";

function OverlaySVG(props) {

  const [modalShow, setModalShow] = useState(false);

  function truncateTitle(txt) {
    
    const maxChars = 19;
    var title = [""];
    for (let i = 0; i < txt.length; i++) {
      if (i >= maxChars) {
        title += "...";
        break;
      }
      title += txt[i];
    }
    return title;
  }

  function handleClick(){
    console.log(!props.addFlag)
    if(!props.addFlag){
      setModalShow(true);
    }
  }

  return (
    <svg
      width="100%"
      height="100%"
      viewBox="0 0 360 360"
      xmlns="http://www.w3.org/2000/svg"
      
    >
      {/* Custom SVG Component 1: Cardback */}
      <Cardback x="5" y="5" width="350" height="350" />
      {/* Imported Image */}
      <image
        x="77"
        y="27"
        width="205"
        height="125"
        preserveAspectRatio="none"
        xlinkHref={props.img}
      />
      {/* Custom SVG Component 2: ImageMask */}
      <ImageMask x="5" y="5" width="350" height="350" onClick={() => {handleClick()}}/>
      {/* Custom SVG Component 3: TextFields */}
      <TextFields x="5" y="5" width="350" height="350" onClick={() => {handleClick()}} />
      {/* Title Overlay */}
      <text x="70" y="187" fill="#331817" fontSize="25" onClick={() => {handleClick()}} >
        {truncateTitle(props.text)} 
      </text>
      {/* Tags Overlay */}
      {/* <text x="75" y="40" fill="black" fontSize="15">
        user_name | Reading #7 | Rare
      </text> */}
      {/* Reading Overlay: Line 1 */}
      <CardReading txt={props.text2} onClick={() => {setModalShow(true)}}/>
        <LargeModal
        show={modalShow}
        onHide={() => setModalShow(false)}
        text = {props.text}
        text2 = {props.text2}
      />
    </svg>
    
  );
}

function CardReading(props) {
  return (
    <svg style={{ whiteSpace: "pre-line" }}>
      <WrapText
        cardReading={props.txt}
      />
    </svg>
  );
}

function WrapText({ cardReading }) {
  const maxChars = 18;
  let counter = 0;
  let lines = [""];
  let lineCounter = 0;
  // for each char in reading
  for (let i = 0; i < cardReading.length; i++) {
    // if the index of the current char is within the max
    if (counter < maxChars) {
      let temp = [""];
      // get a substring of the string for the current line
      for (let j = i; j < cardReading.length; j++) {
        // push alphanumeric chars
        if (cardReading[j] !== " ") {
          temp.push(cardReading[j]);
          // else, end of word reached if " " found
        } else {
          break;
        }
      }
      // if the substring goes past max chars
      if (temp.length + counter > maxChars) {
        // add word to string
        lines.push(temp.join(""));
        lineCounter++;
        // jump i to end of word
        i += temp.length - 1;
        // update counter to substring length
        counter = temp.length;
      }
      // add next char to output string and update char count for current line
      lines[lines.length - 1] += cardReading[i];
      counter++;
      // counter greater than max chars
    } else {
      // new line
      counter = 1;
      lines.push(cardReading[i]);
    }
    if (lineCounter === 3) {
      lines[lines.length - 1] += "...";
      break;
    }
  }

  const textElements = lines.map((line, index) => (
    <text
      key={index}
      x="90"
      y={240 + index * 20}
      fill="#333333"
      fontSize="18"
      fontFamily="Cinzel"
    >
      {line}
    </text>
  ));

  

  return <svg>{textElements}</svg>;
}



export default OverlaySVG;
