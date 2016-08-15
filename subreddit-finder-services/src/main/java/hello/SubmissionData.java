package hello;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import lombok.Data;
import com.fasterxml.jackson.core.JsonParser;

import java.io.IOException;
import java.time.Instant;
import java.time.OffsetDateTime;

import static java.time.ZoneOffset.UTC;

@Data
public class SubmissionData {
    private String subredditName;
    @JsonProperty("cache_timestamp_utc")
    private String cacheTimestampUtc;
    private String permalink;
    private int score;
    private String url;
    private String author;
    @JsonProperty("created_utc")
    private String createdUtc;

//    public static class OffsetDateTimeDeserializer extends JsonDeserializer<OffsetDateTime> {
//        @Override
//        public OffsetDateTime deserialize(JsonParser json, DeserializationContext arg1) throws IOException {
//            final int seconds = (int)json.getDoubleValue();
//            return OffsetDateTime.ofInstant(Instant.ofEpochSecond(seconds), UTC);
//        }
//    }
}
