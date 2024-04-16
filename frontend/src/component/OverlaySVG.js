import React from "react";
import { ReactComponent as Cardback } from "../Cardback.svg";
import { ReactComponent as ImageMask } from "../ImageMask.svg";
import { ReactComponent as TextFields } from "../TextFields.svg";

function OverlaySVG(props) {
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
      <ImageMask x="5" y="5" width="350" height="350" />
      {/* Custom SVG Component 3: TextFields */}
      <TextFields x="5" y="5" width="350" height="350" />
      {/* Title Overlay */}
      <text x="70" y="187" fill="#331817" fontSize="30">
        {props.text}
      </text>
      {/* Tags Overlay */}
      {/* <text x="75" y="40" fill="black" fontSize="15">
        user_name | Reading #7 | Rare
      </text> */}
      {/* Reading Overlay: Line 1 */}
      <CardReading txt={props.text2}/>
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
  const maxChars = 25;
  let counter = 0;
  let lines = [""];
  for (let i = 0; i < cardReading.length; i++) {
    if (counter < maxChars) {
      let temp = [""];
      for (let j = i; j < cardReading.length; j++) {
        if (cardReading[j] !== " ") {
          temp.push(cardReading[j]);
        } else {
          break;
        }
      }
      if (temp.length + counter > maxChars) {
        lines.push(temp.join(""));
        i += temp.length - 1;
        counter = temp.length;
      }
      lines[lines.length - 1] += cardReading[i];
      counter++;
    } else {
      counter = 1;
      lines.push(cardReading[i]);
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

// function WrapText({ cardReading }) {
//   const maxChars = 22;
//   let counter = 0;
//   let result = "";
//   for (let i = 0; i < cardReading.length; i++) {
//     if (counter < maxChars) {
//       counter++;
//       result += cardReading[i];
//     } else {
//       counter = 0;
//       result += "\n";
//     }
//     console.log(result);
//   }
//   return (
//     <svg>
//       text(x="90", y="240", fill="#333333", fontSize="18", fontFamily="Cinzel"){" "}
//       {result}
//     </svg>
//   );
// }

export default OverlaySVG;
