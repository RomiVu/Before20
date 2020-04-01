class HTTP:
    def start_request(self, server_con, request_con):
        raise NotImplementedError()
    def on_close(self, server_con):
        pass

class ROUTER(HTTP):
    def find_handler(self, request, **kwargs):
        raise NotImplementedError()
    def start_request(self, server_con, request_con):
         return "ROUTINGDELEGATE...OBJECT"

class RE_ROUTER(ROUTER):
    def re_url(self, name, *args):
        raise NotImplementedError()

class RULE_ROUTER(ROUTER):
    def __init__(self, rules=None):
        self.rules = []
        if rules:
            self.rules.append("fuck, this is prcessed rules;")
        print(f"all fucked. RULE_ROUTER FINALLY FINAL __INIT__ {self.rules} ")
    def find_handler(self, request, **kwargs):
        return "fuck HTTPMESSAGGEDELEGATE"

class RE_RULE_ROUTER(RE_ROUTER, RULE_ROUTER):
    def __init__(self, rules=None):
        self.named_rules = {}
        print(f"RE_RULE_ROUTER IS INIITTIANISDN {rules}")
        super(RE_RULE_ROUTER, self).__init__(rules)

    def re_url(self, name, *args):
        return None # much more code here


class _APP_ROUTER(RE_RULE_ROUTER):
    def __init__(self, application, rules=None):
        self.application = application
        print(f"_APP_ROUTER IS INITIZATION { rules }")
        super(_APP_ROUTER, self).__init__(rules)

    def process_rule(self, rule):
        return rule

    def get_target_delegate(self, target, request, **target_params):
        return super(_APP_ROUTER, self).get_target_delegate(target, request, **target_params)


class APP(RE_ROUTER):
    def __init__(self, handlers=None, default_host=None, transforms=None, **kwargs):
        print(f"APP is fucking initization {handlers} ... ")
        self.wild_router = _APP_ROUTER(self, handlers)
        self.default_router = _APP_ROUTER(self, Rule(AnyMatcher(), self.wild_router))

class Rule:
    def __init__(self, matcher, target, target_kwargs=None, name=None):
        self.matcher = matcher
        self.target = target

class Matcher:
    def match(self, request):
        raise NotImplementedError()
    def reverse(self, *args):
        return None

class AnyMatcher(Matcher):
    def match(self, request):
        return {}


if __name__ == "__main__":
    app = APP([1,2,3])

