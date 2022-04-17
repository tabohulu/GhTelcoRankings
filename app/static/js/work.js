"use strict";
let tweets_boundingBox = [];
let tweets_container = document.getElementsByClassName("card-div")[0];
let tweets_container_boundingBox = tweets_container.getBoundingClientRect();
let tweet_card = Array.from(document.getElementsByClassName("card"));
let tweets_navigation = Array.from(document.getElementsByClassName("nav"));
let tweet_card_index = 0;
let tweet_card_index_element = document.getElementById("tweets_index");
let no_of_quotes = Number(tweet_card_index_element.innerText.split("/")[1]);
let sentiment_radios = Array.from(
  document.querySelectorAll("input[type=radio]")
);
let submit_button = document.getElementById("submit");
let form = document.getElementById("form");

tweets_navigation.forEach((card) => {
  card.onclick = scrollToTweet;
});

tweet_card.forEach((s) => {
  tweets_boundingBox.push(s.getBoundingClientRect());
});

sentiment_radios.forEach((radio) => {
  radio.onclick = getSelected;
});

submit_button.style.display = "none";
submit_button.onclick = () => {
  console.log("here");
  form.submit();
};
let sentiments_assigned = 0;

function scrollToTweet(event) {
  if (event.target.id === "left") {
    tweet_card_index =
      tweet_card_index - 1 >= 0 ? tweet_card_index - 1 : tweet_card_index;
    sentiments_assigned - 1 >= 0
      ? sentiments_assigned - 1
      : sentiments_assigned;
  } else {
    tweet_card_index =
      tweet_card_index + 1 < no_of_quotes
        ? tweet_card_index + 1
        : tweet_card_index;

    sentiments_assigned + 1 < no_of_quotes
      ? sentiments_assigned + 1
      : sentiments_assigned;
  }
  tweets_container.scrollTo(
    tweets_boundingBox[tweet_card_index].x - tweets_boundingBox[0].x,
    tweets_container_boundingBox.y
  );
  tweet_card_index_element.innerText = `${
    tweet_card_index + 1
  }/${no_of_quotes}`;
}

function getSelected() {
  sentiments_assigned += 1;

  //move to next question
  tweet_card_index =
    tweet_card_index + 1 < no_of_quotes
      ? tweet_card_index + 1
      : tweet_card_index;

  scrollAction();

  //make button active if all questions answered
  if (sentiments_assigned >= no_of_quotes) {
    submit_button.enabled = false;
    submit_button.style.display = "flex";
  }
}

function scrollAction() {
  tweets_container.scrollTo(
    tweets_boundingBox[tweet_card_index].x - tweets_boundingBox[0].x,
    tweets_container_boundingBox.y
  );
  tweet_card_index_element.innerText = `${
    tweet_card_index + 1
  }/${no_of_quotes}`;
}
