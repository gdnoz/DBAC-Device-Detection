class SxcRule:
    id = ''
    device = ''
    domain = ''
    shares = []
    provides = []
    requires = []

    def __init__(self,
                 id: str,
                 device: str,
                 domain: str,
                 shares: list,
                 provides: list,
                 requires: list):
        self.id = id
        self.device = device
        self.domain = domain
        self.shares = shares
        self.provides = provides
        self.requires = requires
        

class SxcContract:
    id = ''
    rules = []

    def __str__(self):
        ret = "Security contract {}:\n".format(self.id)

        for rule in self.rules:
            ret += "\tRule {}:\n".format(rule.id)
            ret += "\t\tDevice:     {}\n".format(rule.device)
            ret += "\t\tDomain:     {}\n".format(rule.domain)
            ret += "\t\tShares:     {}\n".format(rule.shares)
            ret += "\t\tProvides:   {}\n".format(rule.provides)
            ret += "\t\tRequires:   {}\n".format(rule.requires)

        return ret

    def __init__(self, id: str, rules: list):
        self.id = id
        self.rules = rules