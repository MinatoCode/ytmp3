import { youtube } from 'btch-downloader';

export default async function handler(req, res) {
  const url = req.query.url;

  if (!url) {
    return res.status(400).json({
      success: false,
      author: "minato",
      download_url: null,
      message: "Please provide a YouTube URL (?url=...)"
    });
  }

  try {
    const data = await youtube(url);

    if (!data || data.status === false || !Array.isArray(data.audio) || data.audio.length === 0) {
      return res.status(400).json({
        success: false,
        author: "minato",
        download_url: null,
        message: data?.message || "Failed to fetch audio"
      });
    }

    const mp3Url = data.audio[0].url; // first audio stream

    return res.status(200).json({
      success: true,
      author: "minato",
      download_url: mp3Url
    });

  } catch (err) {
    console.error(err);
    return res.status(500).json({
      success: false,
      author: "minato",
      download_url: null,
      message: "Internal server error"
    });
  }
  }
                                
