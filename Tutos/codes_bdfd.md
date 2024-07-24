# Comando Play:

Por favor esperar un poco si demora.

```python
$nomention
$var[dominio;tu url de render]

$onlyIf[$message!=;Escribe algo para escuchar]

$var[json;{
    "guild_id": $guildID,
    "channel_id": $channelID,
    "user_id": $authorID,
    "url": "$url[encode;$message]"
}]
$httpPost[$var[dominio]/api/musica/;$var[json]]
$if[$httpResult[status]==400]
Conectate. aun canal de voz $username.

$stop
$elseif[$httpResult[status]==201]
$description[La canción ya se agrego a la lista con exito]
$stop
$elseif[$httpResult[status]==200]

$httpGet[$var[dominio]/api/youtube_info/?music=$httpResult[data]]

$title[$httpResult[data;0;title]]
$description[
Canal: $httpResult[data;0;channel]
]
$thumbnail[$httpResult[data;0;thumbnails;0]]

$addField[Duración;
$httpResult[data;0;duration]]

$addField[Canal;
$httpResult[data;0;channel]]

$addField[Vistas;
$httpResult[data;0;views]]
$endif
```
