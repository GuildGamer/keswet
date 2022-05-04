from rest_framework import permissions
from . import serializers as sz
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework import parsers
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = sz.UserDetailSerializer
    queryset = User.objects.all()
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    search_fields = ["email", "phone", "first_name", "last_name"]

    @action(
        methods=["POST"],
        detail=False,
        url_path="signup",
        permission_classes=[permissions.AllowAny],
    )
    def signup(self, request) -> Response:
        """
        Sign up view
        """
        serializer = sz.UserSignUpSerializer(
            data=request.data, context={"request": request}
        )
        if not serializer.is_valid():
            return Response(
                {"success": False, "error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.data
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        password = data.get("password")
        phone = data.get("phone")

        try:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "phone": phone,
                    "first_name": first_name,
                    "last_name": last_name,
                },
            )

        except Exception as e:
            print(f"ERROR {e}")
            return Response(
                {"success": False, "error": f"{e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        if not created:
            return Response(
                {
                    "success": False,
                    "error": "Looks like you already have an account, sign in instead?",
                },
                status=status.HTTP_409_CONFLICT,
            )
        user.set_password(password)

        user.save()

        return Response(
            {"success": True, "data": sz.UserDetailSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )


class UserAuthViewSet(viewsets.ModelViewSet):
    """
    Account signin
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = sz.UserDetailSerializer
    queryset = User.objects.all()
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)

    @action(
        methods=["POST"],
        detail=False,
        url_path="signin",
        permission_classes=[permissions.AllowAny],
    )
    def signin(self, request) -> Response:
        serializer = sz.UserSignInSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "error": serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        data = serializer.data
        email = data.get("email")
        password = data.get("password")

        try:
            user: User = User.objects.get(email=email)  # tid=tenant.tid
        except User.DoesNotExist:
            return Response(
                {"success": False, "error": "Please check your username and password"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "error": "something wrong happened, please try again later",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.check_password(password):
            return Response(
                {"success": False, "error": "invalid credentials"},
                status=status.HTTP_403_FORBIDDEN,
            )

        token = Token.objects.create(user=user)
        user.token = token.key
        user.save()
        user.refresh_from_db()
        data = sz.UserDetailSerializer(user).data
        data["token"] = user.token
        data["timestamp"] = timezone.now().timestamp()
        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
