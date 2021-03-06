import React, { useState, useMemo, useRef, useEffect } from 'react'
import ReactLoading from 'react-loading';
import 'bootstrap/dist/css/bootstrap.min.css';
import TinderCard from 'react-tinder-card'
import './../css/CardReview.css'
import axios from 'axios'
import { useCookies } from 'react-cookie';
import { useNavigate } from 'react-router-dom';

class PictureData {
  name: string = '';
  key?: string = '';
  url: string = '';
}

const db: PictureData[] = [];
const revDb: PictureData[] = [];
let revIndex = 0;

function ImageSlideShow() {
  let swipeDir;
  let navigate = useNavigate();

  const [isLoading, setLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(revDb.length - 1)
  const [lastDirection, setLastDirection] = useState('')
  const currentIndexRef = useRef(currentIndex)
  const [cookies, setCookie, removeCookie] = useCookies(['google-token']);

  const images = [
    'https://holland2stay.com/media/pictures/LT2/LT2-0.jpg',
    'https://holland2stay.com/media//pictures/DOK/DOK-0.jpg',
    'https://holland2stay.com/media/pictures/VHS/VHS-0.jpg',
    'https://holland2stay.com/media/pictures/WFC/WFC-0.jpg'
  ];

  useEffect(() => {
    if (!('google-token' in cookies)){
      navigate('/login');
    }

    // To Test: console.log("cookies", cookies["google-token"]);
    
    getImages();
    // OR
    // getRandom();
  }, []);

  const getImages = () => {
    for (let i in images) {
      db.push({ name: `img_${i}`, url: images[i] });
    }
    for (let tempUrl of Array.from(db).reverse()) {
      revDb.push(tempUrl);
    }
    setLoading(false);
  }

  const getRandom = () => {
    const randomNumber = Math.floor(Math.random() * 10) + 10; // Between 10 and 20

    axios.get(`https://api.pexels.com/v1/search?query=cat&per_page=${randomNumber}`, {
      headers: { "Authorization": "563492ad6f91700001000001992684dff806482995da956a82ac603c" }
    })
      .then((res) => {
        for (var i in res.data.photos) {
          db.push({ name: `img_${i}`, url: res.data.photos[i].src.original });
        }
        for (let tempUrl of Array.from(db).reverse()) {
          revDb.push(tempUrl);
        }
        setLoading(false);
      })
  }


  const Loading = () => (
    <ReactLoading type={'bars'} color={'#ffffff'} height={667} width={375} />
  );

  const childRefs:React.Ref<any>[] = useMemo(
    () =>
      Array(revDb.length)
        .fill(0)
        .map((i) => React.createRef()),
    []
  )

  // set last direction and decrease current index
  const swiped = async (direction: string, nameToDelete: string, index: number) => {
    if (direction === "right") {
      swipeDir = ("Yey, we are glad you liked it.");
    }
    setLastDirection(direction);
    revIndex = revIndex + 1;

    if (revIndex >= db.length) {
      window.location.reload();
    }
  }

  if (isLoading) {
    return (<Loading />)
  }

  return (

    <div className="fullC">
      <h1>Swipe left or right on new apartments</h1>
      <div className="row">
        <img src="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/apple/285/cross-mark_274c.png" height="220px" className="directionF" />
        <div className='cardContainer'>
          {revDb.map((character, index) => (
            // @ts-ignore
            <TinderCard
              ref={childRefs[index]}
              className='swipe'
              key={character.name}
              onSwipe={(dir) => swiped(dir, character.name, index)}
            >
              <div className='card-wrapper'>
                <img className='card' src={character.url} />
              </div>
              </TinderCard>
          ))}
        </div>
        <img src="https://emojipedia-us.s3.amazonaws.com/source/skype/289/check-mark_2714-fe0f.png" height="300px" className="directionFN" />
      </div>
      <div className='buttons'>

      </div>

      <h2 className='infoText'>
        {swipeDir}
      </h2>

      <h2 className='infoText'>
        Swipe left if you don't like the image or right if you think it looks awesome!
      </h2>
    </div>
  )
}

export default ImageSlideShow
