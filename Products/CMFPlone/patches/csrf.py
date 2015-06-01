# -*- coding: utf-8 -*-
from plone.protect import CheckAuthenticator
from plone.protect import protect

# apply csrf-protection decorator to the given callable
patch = protect(CheckAuthenticator)


def applyPatches():
    """ apply csrf-protection decorator to all relevant methods """

    from Products.CMFPlone.PloneTool import PloneTool as PT
    PT.setMemberProperties = patch(PT.setMemberProperties)
    PT.changeOwnershipOf = patch(PT.changeOwnershipOf)
    PT.acquireLocalRoles = patch(PT.acquireLocalRoles)
    PT.deleteObjectsByPaths = patch(PT.deleteObjectsByPaths)
    PT.transitionObjectsByPaths = patch(PT.transitionObjectsByPaths)
    PT.renameObjectsByPaths = patch(PT.renameObjectsByPaths)

    from Products.CMFCore.RegistrationTool import RegistrationTool
    RegistrationTool.addMember = patch(RegistrationTool.addMember)

    from Products.CMFCore.MembershipTool import MembershipTool as MT
    MT.setPassword = patch(MT.setPassword)
    MT.setRoleMapping = patch(MT.setRoleMapping)
    MT.deleteMemberArea = patch(MT.deleteMemberArea)
    MT.setLocalRoles = patch(MT.setLocalRoles)
    MT.deleteLocalRoles = patch(MT.deleteLocalRoles)
    MT.deleteMembers = patch(MT.deleteMembers)

    try:
        # XXX CMF 2.3 compatibility, but does it still make sense?
        from Products.CMFCore.MemberDataTool import MemberAdapter as MD
    except ImportError:
        from Products.CMFCore.MemberDataTool import MemberData as MD
    original_setProperties = MD.setProperties

    def setProperties(self, properties=None, REQUEST=None, **kw):
        return original_setProperties(self, properties, **kw)

    setProperties.__doc__ = original_setProperties.__doc__
    MD.setProperties = patch(setProperties)

    from Products.CMFPlone.RegistrationTool import RegistrationTool
    RegistrationTool.editMember = patch(RegistrationTool.editMember)

    from Products.PluggableAuthService.PluggableAuthService import \
         PluggableAuthService as PAS
    PAS.userFolderAddUser = patch(PAS.userFolderAddUser)
    PAS.userFolderEditUser = patch(PAS.userFolderEditUser)
    PAS.userFolderDelUsers = patch(PAS.userFolderDelUsers)
