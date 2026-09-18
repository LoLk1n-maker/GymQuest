from Profiles.models import Profile

def user_profile(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = None
        return {'user_profile': profile}
    return {'user_profile': None}