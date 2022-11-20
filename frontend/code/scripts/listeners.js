const baseUrl = "host:port";

const sendControls = async () => {
    const urlToFetch = tmdbBaseUrl + movieEndpoint + requestParams;
    try{
      const response = await fetch(urlToFetch, { cache: "no-cache" });
      if(response.ok){
        const movieInfo = await response.json();
        return movieInfo;
      }
    }catch(error){
      console.log(error);
    }
}

