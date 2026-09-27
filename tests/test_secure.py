# This file is part of ChemPy.
# Copyright (C) 2026 Chem
#
# ChemPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ChemPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ChemPy. If not, see <http://www.gnu.org/licenses/>.

import pytest
from pgpy import PGPKey
from chempy.secure import (
    generate_pgp_keypair,
    string_to_pgpkey,
    generate_password
)
@pytest.fixture
def str_private_key():
    return """-----BEGIN PGP PRIVATE KEY BLOCK-----

xcZYBGq5VIIBEAC8+FcOPUSXUoMxuDC5XNza6z19C4bGoNWQlUDgjuGMDMhzwoxI
Mo5lStZAqhN0+SfK0k4YuKHxJW9eDGzmZRdJSrDSC9f7ax1099fU8vPBJHaCsrWO
uxatdU9C1VxyxXFC6IhFZY0hUCmrJ3765szz1AVT2hqXAvdmCVneuqHFnTVWAEth
bsRz5WNSMbDyEqPB81T2bmZglGmkhcH/8WTcJdxvOD6pMfF7CR3VBoEadVqHh7er
xmQgAuqWzy7sgbCqRAJSQQglCvEAZuFHMEQ19W1Ey5vHPfwqsBC1wfu6RAPv88nL
7OW8o/xvQJFZqoWUvtmHSq+DIB6vsh3tt6EzVUH6qa0dFlU+8HbnrTIkyzdziSJL
IXCXmNnVtV46Sn2UKtxLHavv6pQSse5G7X0nlzykqk0+z7n9k20y7PJZ7QTZjX4a
ggqAwlrI0Re7yUXelPQEGLQZPQl37kai8ItQq+CaGGawcXgd/LJh1yT1JADDrn8K
IK9A1Lz2sWbfQG0vDKsRg7ycmj4RplNDkr1YO7sMTi1wwipydMGWZpsP8/XwokTz
JvLEA2vnIKh09w95x4fZxuKLFvs6wvcfD2Umo734pFJI31wdK2WnQJrWXt48Kg6e
GbcFO94k8qXi/EP0OHMHDQqX3AHjNYRTvqgPq8T3p9uOLpaFOykWA8ux8wARAQAB
AA/+OuafX/lZ5V7bNMaoLUbUMkprrovGtSfRmZDkGXp/tAMSAf8Mcb6MYuc6NAqv
KOE2dYIqxIrcM0mLVoHB+ehdo0MsLTRy3FONaXWNKTuXHccrR17Dt5r6HRP5IihV
+hIv1P6c5yCZpl4Rtt8HNdZ14LRf+rx7WEGc8omMoR+EKA/x3X4XAOYhRsyjsi15
7WJA98XMYEmWEJmB+j2U9B1+Zh5JAMPDyEIgdkynp0wxNpmIn8D+T4T1lYLDM0Gd
6ysbcV7kaFYL31vzNcBbjLBvOnBm4DAkvKxF6tpZQwYVXAAyR/sxlaYgD7X/i3/R
LmU34N7B9+kgHtuGpRX8PSnlDQzNlewYq3PgvPCnwWV0em6h9HLiIgk+mXwEidic
FYXlNliE9Yq1DrIePDNqJyufJvmR9iDtOb5ack2BYD36asK++Cq3F1X86GML85va
WbDSVD7GKiIpuketWRJfHOUhWl4mjnTNC+fd31oMzQ/4pH0PTiFtbCKd7ScyZ9wd
TbNhNLhvxAj89q1f5EIJgVQxaBYzJUGFrF3QaIt/X7v4S/rvQ7DTcCy9KeJupVVg
/4c34v4NEVHMYXQjXQ1NGatYuKTGFHpMMFDDXMr/ADo1dEYUg7kV/Qjn5/V1MAwF
Rax7ePzkRRrXDXhSP5AeAgUmGjq9upRaY59V4qpW96+mf5EIAPJjpZM/vmdjI1KT
djT0noILmyWPLxyAv2ciNbMjfxLN6CyMmuHg6avcfk1Oa13qV2GGaZ+1QW0AUTxa
+lwB4nV2W0BTqKjru6GnJsNVGlyCMMFcxapNFps1JEVbLGFDkwy16niwhH52lg6k
Lekm5bWiefts3eioNMcOfIcEDNmYnzH9MDbTSbE95DB4yP/Ubiadt7T7ewfnO/Gk
bsmd6vCHgPmPBLFJI4G7TzUCcWG3xR5cWJc0ikiItcMxgHsXmBRE1fArbvwK0WOb
WKY/yas+mwz2HIsk/K1IMc9qxdLQI4V4JjUpJ7j7EyumMd5OyFNuPef3gD436DY2
zV0GRCMIAMeUyoFMz49EtZtJHAXkfDcB4v5AWsTol4B82EUTn4cuSYNXnT0yBvNr
L6OgEdPoOY1UvAX/ChEx9frAQ5cKXH7vZiy98OEH+1+ldQ2nfeAVsdXkPg61dLHJ
lwRruEZtiaHWR+QX1pTcdU1HZ4IrciTmvDvjymFLiCHp92yFs3uNqQEgwZQU1VWC
Xawe2XiNQ3EEGPsidYL2CrhGs7ylBPDX2tbCI0SNHWaLe4QhBJoeT+wPNW5k6z0I
egAG5lBZT+f45b4jRZO+GwHV295j6pOE1o/ZiXJ8l7gr+MZDe6HVjCGd289s/FKg
jUzmskHMCXHRLeI95cbk+GNjCPYyj/EIAKH4WDN/DIeEg6O4l3qHdtLXthyOi9bP
0wH09w+Yj7gubkkTxL3TA9sIpZ06u6eudVdXV2PjgmydERmozDq4XAPOgdxRkebx
bDedW6MdkHLbRDEQXFzSx+SmZcFShfqrtwHKPDoQDUQflF+43DZVXjJe04Ov4flZ
yVkA86SwPu5Bo3PpuRLpTiIVRi4onfe3j7pZmTA+gUlNSlW0kUQYuVDLIKP/V/RQ
3N0+O3WiV5RNHep6JJN7UuIOpLGLOKAFMvvCKeCfSERGnbbA3JFRCJgep4Q4sZ2e
QEKO3/o+g6LurxJPuFl5/yCFGcH1IBJl+AQ2S+OpmMQw1V+aWPUqRvh2Xc0fVXNl
ciAoTm9uZSkgPGVtYWlsQGV4YW1wbGUuY29tPsLBgAQTAQgAKgUCarlUhAIbBgIL
CQMVCAoCHgEWIQT14nYLAbAc55V9oDklp1nxTMxG3gAKCRAlp1nxTMxG3peXD/48
X+RYs2KSm2psUT9CRGDpumPPrk6DJNw6rcOfXOV0u2T3gntNVbELIyv33DteCv1F
VP39w9VyyetuCwySMSDSzEtP2pOCR1o139qVNBmaqXIQ3ZMeElnYe2fqUsGPM6I5
DRIbPHb/H7aN/LkPi1dvwtRPC1cpp6nprdAm+2erE724DqfTMcLMiJJJyAgiE9Xa
pf8If48Ffnrm5Wp3T2Q8mcpOTu3xAwm3/LQZX09UW4XrWP9cbK2aQtsT5HGIOlVz
PxbfWST42tGVyh0ygv+LjSYZcFSvzjfA82fe1jyVXIDlfqa0k0fOUv8uPdYi9mXP
xxTT9EURY68CO4GlFXOsXxj51mBGUR+iPCvoFuCHXXqsSo8cJ6Z/Y8+0qVBYbE/n
nu9qjV98LcDlLOdL3uh3tO8S8ZmkO/Pehnam1nVnmJA968VRxWs507DcuiqgEjXC
I4bPaigCil4g3k0xND+cP5xn6ZDLlNWthhFefgHTUOQC6RaeAzEiFYc6ekqNU42/
jYT1fAAhPfipNpn7jEHjaXUWFHZo90qtUowpcDtMl9CFMEBOsZ9YEObkVKwRe3pO
76i6R1z5ZK0Fj5xMBXv9DsH+/+t9717pKEocFx8LZ2MqHDEw8lW748s9rt/hfFI4
aoTaHhia6Y9lQdzV5vD5BC6LeSe30khHJbBrCnmyHw==
=lkRK
-----END PGP PRIVATE KEY BLOCK-----

"""

## Smoke Tests

def test_generate_pgp_keypair():
    private_key, public_key = generate_pgp_keypair()
    private_key_lines = private_key.split('\n')
    public_key_lines = public_key.split('\n')
    assert private_key_lines[0] == '-----BEGIN PGP PRIVATE KEY BLOCK-----'
    assert public_key_lines[0] == '-----BEGIN PGP PUBLIC KEY BLOCK-----'


def test_string_to_pgpkey(str_private_key):
    assert isinstance(string_to_pgpkey(str_private_key), PGPKey)


def test_generate_password():
    password = generate_password()
    ## Check default length
    assert len(password) == 16
    assert isinstance(password, str)


## Functional Tests

def test_generate_password_specified_length():
    assert len(generate_password(length=8)) == 8
