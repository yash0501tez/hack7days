import smartpy as sp
FA2 = sp.io.import_script_from_url("https://smartpy.io/templates/fa2_lib.py")

class NFTCertificate(
    FA2.Admin,
    FA2.ChangeMetadata,
    FA2.OnchainviewBalanceOf,
    FA2.BurnNft,
    FA2.WithdrawMutez,
    FA2.Fa2Nft
):
    def __init__(
        self, 
        admin, 
        metadata, 
        token_metadata = {}, 
        ledger = {}, 
        policy = None, 
        metadata_base = None,
        users_address = {}
    ):
        FA2.Fa2Nft.__init__(
            self,
            metadata,
            token_metadata = token_metadata,
            ledger = ledger,
            policy = policy,
            metadata_base = metadata_base,
        )
        FA2.Admin.__init__(self, admin)
        self.update_initial_storage(
            users_address = users_address
        )

    @sp.entry_point
    def mint(self, _to, _metadata):
        sp.set_type(_metadata, sp.TBytes)
        sp.verify(
            ~self.data.users_address.contains(sp.sender), 
            message = "User already minted Certificate"
        )
        
        token_id = sp.compute(self.data.last_token_id)
        token_details = sp.record(
            token_id = token_id,
            token_info = sp.map(
                l = {
                    '': _metadata
                }
            )
        )
        
        self.data.token_metadata[token_id] = token_details
        self.data.ledger[token_id] = sp.sender
        self.data.last_token_id += 1
        self.data.users_address[sp.sender] = token_id

metadata_base = {
    "version": "1.0.0",
    "description" : "This implements FA2 (TZIP-012) using SmartPy.",
    "interfaces": ["TZIP-012", "TZIP-016"],
    "authors": ["SmartPy <https://smartpy.io/#contact>"],
    "homepage": "https://smartpy.io/ide?template=FA2.py",
    "source": {
        "tools": ["SmartPy"],
        "location": "https://gitlab.com/SmartPy/smartpy/-/raw/master/python/templates/FA2.py"
    },
    "permissions": {
        "receiver": "owner-no-hook",
        "sender": "owner-no-hook"
    }
}

sp.add_compilation_target(
    "NFT Certificate",
    NFTCertificate(
        admin = sp.address("tz1iWU9xwe1gbboxefyWadcmFeg2yMMLQ8Ap"),
        metadata = sp.utils.metadata_of_url("ipfs://bafkreie7kjyaukhw64ctna64xc5wmwxg6rrb5j2obi2qnsmhrtv2q7yftu"),
        token_metadata = {},
        ledger = {},
        policy = None,
        metadata_base = metadata_base,
        users_address = sp.big_map(
            tkey = sp.TAddress,
            tvalue = sp.TNat,
            l = {}
        )
    )
)
        
@sp.add_test(name="NFT Certificate Test")
def test():
    admin = sp.test_account("admin")
    alice = sp.test_account("alice")
    bob = sp.test_account("bob")
    charlie = sp.test_account("charlie")
    scenario = sp.test_scenario()
    scenario.h1("NFT Certificate")
    nft_certificate = NFTCertificate(
        admin = admin.address,
        metadata = sp.utils.metadata_of_url("ipfs://bafkreie7kjyaukhw64ctna64xc5wmwxg6rrb5j2obi2qnsmhrtv2q7yftu"),
        token_metadata = {},
        ledger = {},
        policy = None,
        metadata_base = metadata_base,
        users_address = sp.big_map(
            tkey = sp.TAddress,
            tvalue = sp.TNat,
            l = {}
        )
    )
    scenario += nft_certificate
    scenario += nft_certificate.mint(
        _metadata = sp.bytes("0x697066733a2f2f6261666b726569667761726262617068656d6479757568613465636162346d356c766d7168676972706f736b6e78656b6a6f616d33327437686f69")
    ).run(sender = alice)
    scenario += nft_certificate.mint(
       _metadata = sp.bytes("0x697066733a2f2f6261666b726569667761726262617068656d6479757568613465636162346d356c766d7168676972706f736b6e78656b6a6f616d33327437686f69")
    ).run(sender = alice)
