import { youtube } from 'btch-downloader';

export default async function handler(req, res) {
  const url = req.query.url;

  if (!url) {
    return res.status(400).json({ success: false, author: "minato", download_url: null });
  }

  try {
    const data = await youtube(url);

    return res.status(200).json({
      success: true,
      author: "minato",
      download_url: data.mp3
    });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ success: false, author: "minato", download_url: null });
  }
}
