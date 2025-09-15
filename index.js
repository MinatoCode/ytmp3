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

    if (!data || data.status === false || !data.mp3) {
      return res.status(400).json({
        success: false,
        author: "minato",
        download_url: null,
        message: data?.message || "Failed to fetch MP3"
      });
    }

    return res.status(200).json({
      success: true,
      author: "minato",
      download_url: data.mp3 // ready-to-download MP3 URL
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
