package hello;

import java.lang.String;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestBody;

@RestController
public class LoginController {

    @RequestMapping(value = "/login", method = RequestMethod.POST)
    public String index(@RequestBody PasswordAuthRequest req) {

        if (isValidPassword(req.user, req.password)) {
            return "Logged In!";
        }

        return "Password Invalid";
    }

    @RequestMapping(value = "/tokenlogin", method = RequestMethod.POST)
    public String index(@RequestBody TokenAuthRequest req) {
        if (isValid(req.token)) {
            return "Authenticated";
        }

        return "Invalid Token";
    }

    private boolean isValid(String token) {
        return token.equals("validtoken");
    }

    private boolean isValidPassword(String user, String password) {
        return password.equals("validpassword");
    }
}